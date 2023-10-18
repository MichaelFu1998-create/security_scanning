def graph_csv(output_directory, resource_path, csv_file, plot_title, output_filename, y_label=None, precision=None, graph_height="600", graph_width="1500"):
  """ Single metric graphing function """
  if not os.path.getsize(csv_file):
    return False, ""
  y_label = y_label or plot_title
  div_id = str(random.random())
  div_string = "<div id=\"%s\" style=\"width:%spx; height:%spx;\"></div>" % (div_id, graph_width, graph_height)
  script_string = """<script type=\"text/javascript\">
        g2 = new Dygraph(
          document.getElementById(\"""" + div_id + """"),
            \"""" + resource_path + '/' + os.path.basename(csv_file) + """",
            {
                        xValueFormatter: Dygraph.dateString_,
                        xValueParser: function(x) {
                                        var date_components = x.split(" ");
                                        var supported_format = date_components[0] + 'T' + date_components[1];
                                        if(date_components[1].indexOf(".") == -1)
                                        {
                                          supported_format += ".0";
                                        }
                                        return Date.parse(supported_format);
                                        },
                        xTicker: Dygraph.dateTicker,
                        xlabel: "Time",
                        ylabel: \"""" + y_label + """",
                        title: \"""" + plot_title + """",
                        labels: ["Time",\"""" + y_label + """"]
            }          // options
        );
        </script>"""

  with open(os.path.join(output_directory, output_filename + '.div'), 'w') as div_file:
    div_file.write(div_string + script_string)
  # TODO(ritesh): Also generate PNGs if someone needs them separately
  return True, os.path.join(output_directory, output_filename + '.div')