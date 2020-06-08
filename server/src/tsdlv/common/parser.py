import re
import logging
import json

class Parser:
  def __init__(self, template):
    self._template = template
  
  def get_iterations(self, text):
    logging.debug('Getting iterations from log text')

    iter_expr = self._template['iter_expr']
    (iter_expr, val_expr) = self._get_val_expr(iter_expr)

    logging.debug(f'iter_expr = {iter_expr}')
    logging.debug(f'val_expr = {val_expr}')
    
    # build the iteration labels and contents
    iterations = []
    splits = re.split(f'({iter_expr})', text)
    # there is an empty string at the beginning of the splits list even when the first thing in the file matches the regex
    i = 1
    while i < len(splits) - 1:
      iteration = {}
      label_split = re.split(f'({val_expr})', splits[i])
      if len(label_split) > 1:
        # expect split to be ['{label text}', '{label value}']
        iteration["label"] = label_split[1]
      else:
        logging.warning(f'No label found in iteration labeled: {splits[i]}')
        iteration['label'] = ''
      i += 1

      iteration["contents"] = splits[i]
      i += 1

      iterations.append(iteration)

    # Parse the contents of each iteration
    var_defs = []
    for iter_var in self._template['iter_vars']:
      var_def = {}
      var_def['name'] = iter_var['var_name']
      iter_expr = iter_var['var_expr']
      (iter_expr, val_expr) = self._get_val_expr(iter_expr)
      var_def['iter_expr'] = iter_expr
      var_def['val_expr'] = val_expr

      logging.debug(f'var config: {var_def}')

      logging.debug(json.dumps(var_def))
      var_defs.append(var_def)
      
    
    for iteration in iterations:
      var_values = {}
      for var_def in var_defs:
        match = re.search(var_def['iter_expr'], iteration['contents'])
        if match:
          val = re.search(var_def['val_expr'], match.group(0))
        if val:
          var_values[var_def['name']] = val.group(0)

      iteration['var'] = var_values

    return iterations

  def _get_val_expr(self, expr):
    match = re.search(r"(.*)(\{)(.+)(\})(.*)", expr)
    if match:
      # return the middle group since it excludes the curlies
      return (match.group(1) + match.group(3) + match.group(5), match.group(3))
    else:
      return ''

  