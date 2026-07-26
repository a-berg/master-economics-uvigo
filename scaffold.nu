# scaffold.nu
# Ejecutar con: nu scaffold.nu

# Función para crear las carpetas base y los archivos Typst
def create_base_structure [] {
    print "🚀 Creando estructura del Máster..."

    # Carpetas principales
    mkdir 00_admin
    mkdir 02_tfm
    mkdir 02_tfm/00_propuesta
    mkdir 02_tfm/01_datos
    mkdir 02_tfm/02_codigo
    mkdir 02_tfm/03_escritos
    mkdir 02_tfm/04_bibliografia
    mkdir 02_tfm/05_recursos
    mkdir 02_tfm/output
    mkdir 03_recursos_comunes
    mkdir 03_recursos_comunes/snippets_codigo

    # Crear el paquete local de Typst
    let typst_dir = "03_recursos_comunes/plantillas_typst"
    mkdir $typst_dir

    # --- lib.typ (Lógica compartida) ---
    # Usamos ' (raw string) para que Nushell no intente interpretar los # de Typst
    let lib_typst = '
// lib.typ - Funciones y configuración compartida (Typst 0.15)

// Colores corporativos UVigo (aproximaciones oficiales)
#let uvigo-blue = rgb("#003366")
#let uvigo-cyan = rgb("#0099CC")
#let uvigo-gray = rgb("#58595B")
#let uvigo-light-gray = rgb("#F2F2F2")

// Estilos base aplicados a todos los documentos
#let base-styles() = {
  set text(
    font: ("New Computer Modern", "Latin Modern Math"), 
    size: 11pt,
    lang: "es"
  )
  set par(justify: true, leading: 0.65em, first-line-indent: 1.25em)
  set heading(numbering: "1.1.")
  
  // Estilo para los títulos
  set heading(where level: 1)[
    #set text(size: 14pt, weight: "bold", fill: uvigo-blue)
    #block(above: 1.5em, below: 1em)
  ]
  set heading(where level: 2)[
    #set text(size: 12pt, weight: "bold", fill: uvigo-cyan)
    #block(above: 1.2em, below: 0.8em)
  ]
  
  // Configuración de ecuaciones
  set math.equation(numbering: "(1)")
}

// Bloque para resaltar resultados de código (R/Julia)
#let data-result(label: "Salida de datos", body) = {
  block(
    width: 100%,
    fill: uvigo-light-gray,
    inset: 10pt,
    radius: 4pt,
    stroke: uvigo-cyan + 0.5pt,
    {
      set text(size: 10pt)
      text(weight: "bold", fill: uvigo-blue)[#label]
      v(4pt)
      body
    }
  )
}
'
    $lib_typst | save -f $"($typst_dir)/lib.typ"

    # --- asignatura.typ (Plantilla corta) ---
    let asignatura_typst = '
// Plantilla para trabajos de asignatura
#import "lib.typ": *

#let asignatura(
  title: "Título del trabajo",
  author: "Tu Nombre",
  course: "Máster en Economía",
  subject: "Nombre de la Asignatura",
  doc
) = {
  base-styles()
  
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #subject #h(1fr)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
        #h(1fr) #counter(page).display("1 / 1") #h(1fr)
      ]
    }
  )

  // Portada sencilla
  {
    set par(first-line-indent: 0em)
    v(3cm)
    set text(size: 22pt, weight: "bold", fill: uvigo-blue)
    align(center, title)
    v(1cm)
    set text(size: 12pt, fill: uvigo-gray)
    align(center, [Autor: #author])
    align(center, [#course — #subject])
    v(2cm)
    line(length: 100%, stroke: uvigo-blue + 1.5pt)
  }

  doc
}
'
    $asignatura_typst | save -f $"($typst_dir)/asignatura.typ"

    # --- tfm.typ (Plantilla larga) ---
    let tfm_typst = '
// Plantilla para el TFM
#import "lib.typ": *

#let tfm(
  title: "Título del TFM",
  author: "Tu Nombre",
  advisor: "Nombre del Director",
  year: "2024/2025",
  doc
) = {
  base-styles()
  
  // Márgenes tipo libro (izquierdo más amplio para encuadernación)
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 2.5cm, inner: 3.5cm, outer: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #text(italics)[Máster en Economía — Universidade de Vigo] #h(1fr)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #counter(page).display("1") #h(1fr)
      ]
    }
  )
  
  // Ajustar numeración de headings para TFM (1.1.1)
  set heading(numbering: "1.1.1")

  // --- PORTADA ---
  {
    set par(first-line-indent: 0em)
    v(2cm)
    align(center, text(size: 14pt, fill: uvigo-cyan)[Universidade de Vigo])
    align(center, text(size: 12pt, fill: uvigo-gray)[Facultade de Ciencias Económicas e Empresariais])
    v(2cm)
    align(center, text(size: 12pt, weight: "bold")[MÁSTER UNIVERSITARIO EN ECONOMÍA])
    v(1.5cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(1cm)
    align(center, text(size: 24pt, weight: "bold", fill: uvigo-blue)[#title])
    v(1cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(2cm)
    align(center, text(size: 12pt)[Presentado por: *#author*])
    v(0.5cm)
    align(center, text(size: 12pt)[Director/a: *#advisor*])
    v(2cm)
    align(center, text(size: 12pt, fill: uvigo-gray)[#year])
  }
  
  pagebreak()
  
  // --- ÍNDICE ---
  {
    set par(first-line-indent: 0em)
    heading(level: 1)[Índice]
    outline(title: none, indent: 1.5em, depth: 3)
  }
  
  pagebreak()
  
  doc
}
'
    $tfm_typst | save -f $"($typst_dir)/tfm.typ"

    print "✅ Estructura base y plantillas Typst creadas."
}

# Comando personalizado para crear una asignatura nueva
export def "main new-assign" [name: string] {
    let safe_name = $name | str snake-case | ^iconv -f UTF-8 -t ASCII//TRANSLIT
    let dir = $"01_asignaturas/($safe_name)"

    mkdir $"($dir)/datos"
    mkdir $"($dir)/src/julia"
    mkdir $"($dir)/src/r"
    mkdir $"($dir)/notas"
    mkdir $"($dir)/entregas"
    mkdir $"($dir)/output"

    # Usamos un placeholder y str replace para inyectar la variable sin romper el raw string de Typst
    let ejemplo_typst = '#import "../../03_recursos_comunes/plantillas_typst/asignatura.typ": *

#show: asignatura.with(
  title: "Ejercicio 1",
  author: "Tu Nombre",
  subject: "{{NOMBRE_ASIGNATURA}}"
)

== Planteamiento del problema
Aquí va el enunciado o tus notas.

== Resolución
Aquí pones la matemática: $ integral_0^infinity e^(-x) dif x = 1 $.

== Resultados computacionales
Aquí importarías la imagen generada por R o Julia.

#data-result(label: "Salida del modelo OLS")[
  - Coeficiente $beta$: 0.85
  - P-valor: 0.002
]
'
    let ejemplo_final = $ejemplo_typst | str replace "{{NOMBRE_ASIGNATURA}}" $name
    $ejemplo_final | save -f $"($dir)/entregas/ejercicio_1.typ"

    print $"🎨 Asignatura creada: ($name)"
    print $"   -> Editar: ($dir)/entregas/ejercicio_1.typ"
}

# --- LA MAGIA ESTÁ AQUÍ ---
# Si ejecutas "nu scaffold.nu" sin argumentos, entra por aquí.
export def main [] {
    create_base_structure
}
