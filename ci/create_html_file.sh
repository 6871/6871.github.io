#!/usr/bin/env bash
# Generate graph HTML file

##############################################################################
# Main function to coordinate building file
function main() {
  if [[ $# -lt 2 ]]; then
    printf 'USAGE: output_file graph_div_file...\n'
  fi

  local output_file="${1}"
  local graph_divs=("${@:2}")

  # Write HTML file head; see: man strftime
  {
    cat ci/html/index_head_1.txt
    printf ' %s' "$(date +'%^a %Y-%^b-%d %T %Z')"
    cat ci/html/index_head_2.txt
  } > "${output_file}"

  # Write any graph DIV sections
  local graph_div
  for graph_div in "${graph_divs[@]}"; do
    cat "${graph_div}" >> "${output_file}"
  done

  # Write HTML file tail
  cat ci/html/index_tail_1.txt >> "${output_file}"
}

# Run the script
main "$@"
