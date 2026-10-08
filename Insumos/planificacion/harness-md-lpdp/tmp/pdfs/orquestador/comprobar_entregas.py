from pathlib import Path
from urllib.parse import unquote, urlsplit
import json, re, hashlib
ROOT = Path(__file__).resolve().parents[3]
manifest = json.loads((Path(__file__).parent / "originales.json").read_text())
report = {"originales_sin_cambios": [], "fuentes": []}
for source in manifest:
    p=ROOT/source["source"]
    report["originales_sin_cambios"].append({"ruta": source["source"], "coincide_sha256": hashlib.sha256(p.read_bytes()).hexdigest()==source["sha256"]})
for directory in sorted((ROOT/"Fragmentador-de-Fuentes/Fuentes").glob("*/")):
    files=list(directory.rglob("*.md"))
    broken=[]
    for p in files:
        content=p.read_text()
        for match in re.finditer(r"\[[^\]\n]*\]\(([^)]+)\)", content):
            target=match.group(1).strip()
            if target.startswith("<") and ">" in target:
                target=target[1:target.index(">")]
            target=unquote(target.split("#")[0])
            if not target or urlsplit(target).scheme:
                continue
            candidate=Path(target) if target.startswith("/") else p.parent/target
            if not candidate.exists():
                broken.append({"archivo": str(p.relative_to(ROOT)), "destino": target})
    tree=directory/"ARBOL.md"
    content=tree.read_text() if tree.exists() else ""
    tree_body = content.split("```")[1] if "```" in content else content
    tree_paths = re.findall(r"-> ([^\s#]+\.md)", tree_body)
    missing_tree_paths = [rel for rel in tree_paths if not (directory/rel).is_file()]
    unlisted = [str(p.relative_to(directory)) for p in files if p.parent != directory and p.relative_to(directory).as_posix() not in content]
    report["fuentes"].append({"carpeta": str(directory.relative_to(ROOT)), "markdown":len(files), "articulo_md":sum(p.name=="articulo.md" for p in files), "entregables":{name:(directory/name).exists() for name in ["FUENTE.md", "ARBOL.md", "INFORME-FRAGMENTACION.md"]}, "estados_arbol":{state:len(re.findall(r"\["+state+r"(?:;[^\]]*)?\]",tree_body)) for state in ["completo","parcial","pendiente"]}, "enlaces_rotos":broken, "rutas_del_arbol_inexistentes":missing_tree_paths, "archivos_fuera_del_arbol":unlisted})
output=Path(__file__).parent/"comprobacion-entregas.json"
output.write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
