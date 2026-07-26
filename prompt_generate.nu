#!/usr/bin/env nu

def main [index: int] {
    let contenidos_materias = (open biblio_basica.yaml).asignaturas | get $index
    let prompt_template = open ./prompt.txt

    $prompt_template
    | str replace "{{NAME}}" $contenidos_materias.nombre
    | str replace "{{BIBLIO}}" (
        $contenidos_materias.referencias
        | values
        | flatten
        | to md
    )
    | str replace "{{TOC}}" $contenidos_materias.toc
    | str replace "{{DOC}}" ($contenidos_materias.docentes | to md)
}
