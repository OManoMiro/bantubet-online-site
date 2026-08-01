from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, urlunparse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

BASE_DIR = Path(__file__).resolve().parent
RAIS_DIR = BASE_DIR / "rais"
ARTIGOS_DIR = RAIS_DIR / "artigos"
BLOG_FILE = RAIS_DIR / "blog.html"

app = FastAPI(title="Bantubet Blog Publisher Agent")


class GerarArtigoRequest(BaseModel):
    tema: str
    titulo: Optional[str] = None


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower())
    text = re.sub(r"\s+", "-", text.strip())
    text = re.sub(r"-+", "-", text)
    return text or "artigo"


def ensure_git_auth() -> None:
    subprocess.run(["git", "config", "user.name", os.getenv("GIT_AUTHOR_NAME", "Render Bot")], cwd=BASE_DIR, check=False)
    subprocess.run(["git", "config", "user.email", os.getenv("GIT_AUTHOR_EMAIL", "render-bot@users.noreply.github.com")], cwd=BASE_DIR, check=False)
    subprocess.run(["git", "config", "credential.helper", "store"], cwd=BASE_DIR, check=False)
    subprocess.run(["git", "config", "core.askPass", ""], cwd=BASE_DIR, check=False)

    remote_url = os.getenv("GIT_REMOTE_URL")
    if not remote_url:
        try:
            remote_url = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=BASE_DIR, text=True).strip()
        except subprocess.CalledProcessError:
            remote_url = ""

    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN") or os.getenv("GIT_TOKEN")
    username = os.getenv("GITHUB_ACTOR") or os.getenv("GIT_USERNAME") or "x-access-token"

    if remote_url and token:
        parsed = urlparse(remote_url)
        if parsed.scheme and parsed.netloc and "@" not in parsed.netloc:
            netloc = f"{username}:{token}@{parsed.netloc}"
            remote_url = urlunparse(parsed._replace(netloc=netloc))
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=BASE_DIR, check=False)

    if remote_url:
        subprocess.run(["git", "config", "--global", "url.https://github.com/.insteadOf", "git@github.com:"], cwd=BASE_DIR, check=False)


def render_article_html(tema: str, titulo: str) -> str:
    hoje = datetime.now().strftime("%d/%m/%Y")
    slug = slugify(titulo or tema)
    texto = "\n".join(
        [
            f"<p class=\"text-gray-700\">Este artigo foi gerado automaticamente para o tema \"{tema}\".</p>",
            "<p class=\"text-gray-700\">A proposta é oferecer uma página SEO com visual alinhado ao site da Bantubet, mantendo foco em leitura rápida, clareza e conversão.</p>",
            "<h2 class=\"text-2xl font-black mt-8 mb-3 text-black\">Resumo rápido</h2>",
            f"<p class=\"text-gray-700\">{tema} é um tópico relevante para a audiência do blog e pode ser estruturado em forma de guia útil, destacando benefícios, contexto e próximos passos.</p>",
            "<h2 class=\"text-2xl font-black mt-8 mb-3 text-black\">Dicas de SEO</h2>",
            "<ul class=\"list-disc list-inside text-gray-700 space-y-2\"><li>Use um título curto e direto.</li><li>Inclua palavras-chave no início do texto.</li><li>Adicione links internos para páginas relacionadas.</li></ul>",
        ]
    )

    return f'''<!DOCTYPE html>
<html lang="pt-ao" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo} | Bantubet Blog</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" type="image/png" href="/icons/favicon.png" sizes="48x48">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
    </style>
</head>
<body class="bg-white text-gray-900">
    <header class="fixed top-0 left-0 w-full z-[100] bg-black/90 backdrop-blur-md border-b border-white/10">
        <div class="max-w-7xl mx-auto px-4 md:px-6 h-20 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <a href="/index.html" class="relative group">
                    <img src="/images/logo-bantubet.png" alt="Bantubet" class="h-10 md:h-12 w-auto brightness-110">
                    <div class="absolute -inset-1 bg-[#F5C300] rounded-full blur opacity-20 group-hover:opacity-40 transition"></div>
                </a>
            </div>
            <nav class="hidden lg:flex items-center gap-8 text-sm font-bold text-gray-300">
                <a href="/index.html#benefits" class="hover:text-[#F5C300] transition-colors">Benefícios</a>
                <a href="/index.html#sports" class="hover:text-[#F5C300] transition-colors">Desportos</a>
                <a href="/blog.html" class="hover:text-[#F5C300] transition-colors">Blog</a>
                <a href="/index.html#winners" class="hover:text-[#F5C300] transition-colors">Vencedores</a>
                <a href="/index.html#contact" class="hover:text-[#F5C300] transition-colors">Suporte</a>
            </nav>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-6 pt-28 pb-16">
        <article class="bg-gray-50 rounded-[2rem] p-8 md:p-12 border border-gray-100 shadow-sm">
            <p class="text-xs uppercase tracking-[0.35em] text-[#F5C300] font-black mb-4">Bantubet Blog</p>
            <h1 class="text-4xl md:text-5xl font-black text-black leading-tight mb-4">{titulo}</h1>
            <p class="text-sm text-gray-500 mb-8">Publicado em {hoje}</p>
            <div class="space-y-4 text-lg leading-8 text-gray-800">
                {texto}
            </div>
        </article>
    </main>
</body>
</html>
'''


def create_article_file(tema: str, titulo: str) -> str:
    ARTIGOS_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(titulo or tema)
    target = ARTIGOS_DIR / f"{slug}.html"
    target.write_text(render_article_html(tema, titulo), encoding="utf-8")
    return f"artigos/{target.name}"


def update_blog_list(article_href: str, titulo: str) -> None:
    if not BLOG_FILE.exists():
        raise FileNotFoundError("blog.html não encontrado")

    html = BLOG_FILE.read_text(encoding="utf-8")

    new_post = (
        "<a href=\"{href}\" class=\"block bg-gray-900 rounded-2xl p-5 border border-white/10 hover:border-[#F5C300] transition-colors\">"
        "<span class=\"text-xs uppercase tracking-[0.25em] text-[#F5C300] font-black\">Novo artigo</span>"
        "<h3 class=\"text-xl font-black mt-2 text-white\">{titulo}</h3>"
        "</a>"
    ).format(href=article_href, titulo=titulo)

    marker = "<p class=\"text-gray-300\">Página de blog em construção.</p>"
    replacement = (
        "<p class=\"text-gray-300 mb-8\">Página de blog em construção.</p>"
        "<section class=\"mt-8\">"
        "<h2 class=\"text-2xl font-black text-[#F5C300] mb-4\">Posts recentes</h2>"
        "<div class=\"space-y-3\">{new_post}</div>"
        "</section>"
    ).format(new_post=new_post)

    if marker in html:
        html = html.replace(marker, replacement, 1)
    else:
        html = html.replace("</main>", f"<section class=\"mt-8\">...", 1)

    BLOG_FILE.write_text(html, encoding="utf-8")


def run_git_publish() -> dict:
    ensure_git_auth()

    status = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True, check=False)
    if status.returncode != 0 or not status.stdout.strip():
        return {
            "git": [
                {
                    "command": "git status --porcelain",
                    "returncode": status.returncode,
                    "stdout": status.stdout.strip(),
                    "stderr": status.stderr.strip(),
                    "message": "Nenhuma alteração pendente para publicar.",
                }
            ]
        }

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "Auto-publicação de novo artigo SEO pelo agente"],
        ["git", "push", "origin", "main"],
    ]

    results = []
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"

    for command in commands:
        completed = subprocess.run(command, cwd=BASE_DIR, capture_output=True, text=True, env=env, check=False)
        results.append({
            "command": " ".join(command),
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        })

    return {"git": results}


@app.post("/gerar-artigo")
def gerar_artigo(payload: GerarArtigoRequest):
    tema = (payload.tema or "").strip()
    if not tema:
        raise HTTPException(status_code=400, detail="Informe o tema do artigo.")

    titulo = (payload.titulo or tema).strip()
    href = create_article_file(tema, titulo)
    update_blog_list(href, titulo)

    git_result = run_git_publish()
    return {
        "status": "ok",
        "artigo": href,
        "titulo": titulo,
        "tema": tema,
        "git": git_result,
    }


@app.get("/")
def health():
    return {"status": "ok", "service": "Bantubet Blog Publisher Agent"}
