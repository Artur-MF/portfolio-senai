from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        for attribute in ("href", "src", "srcset"):
            if attribute not in attributes:
                continue
            value = attributes[attribute] or ""
            targets = [value]
            if attribute == "srcset" and value:
                targets = [candidate.strip().split()[0] if candidate.strip() else ""
                           for candidate in value.split(",")]
            for target in targets:
                self.references.append((self.getpos()[0], tag, target.strip()))


def check_reference(root, source, tag, value, documents, external):
    if not value:
        return "URL ou caminho vazio"
    try:
        url = urlsplit(value)
    except ValueError as error:
        return f"URL inválida: {error}"
    if url.scheme in {"mailto", "tel"} and tag == "a":
        return None if url.path else "endereço de contato vazio"
    if url.scheme or url.netloc:
        if url.scheme not in {"http", "https"} or not url.hostname:
            return "URL externa deve usar HTTP ou HTTPS com domínio"
        if value not in external:
            result = subprocess.run(
                ["curl", "--fail", "--silent", "--show-error", "--location",
                 "--proto", "=https,http", "--proto-redir", "=https,http",
                 "--connect-timeout", "8", "--max-time", "20",
                 "--retry", "2", "--retry-max-time", "45", "--output", "/dev/null",
                 "--url", value],
                capture_output=True, text=True,
            )
            external[value] = result.stderr.strip() if result.returncode else None
        return external[value]
    if url.path.startswith("/"):
        return "use um caminho relativo para manter o subdiretório do GitHub Pages"
    target = (source.parent / unquote(url.path)).resolve() if url.path else source
    if not target.is_relative_to(root):
        return "caminho fora do repositório"
    if target.is_dir():
        target /= "index.html"
    if not target.is_file():
        return "arquivo local inexistente"
    if url.fragment and target.suffix.lower() in {".html", ".htm"}:
        if target not in documents:
            documents[target] = Document(target.read_text(encoding="utf-8"))
        if unquote(url.fragment) not in documents[target].ids:
            return "âncora local inexistente"
    return None


def main():
    root = Path.cwd()
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    pages = [root / name for name in tracked if Path(name).suffix.lower() in {".html", ".htm"}]
    documents = {page: Document(page.read_text(encoding="utf-8")) for page in pages}
    external = {}
    errors = []
    for page in pages:
        for line, tag, target in documents[page].references:
            problem = check_reference(root, page, tag, target, documents, external)
            if problem:
                errors.append(f"{page.relative_to(root)}:{line}: {target!r}: {problem}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Links e imagens validados em {len(pages)} arquivo(s) HTML.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
