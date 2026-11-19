/**
 * @file A simple filter query language for searching and filtering data.
 * @author Nurul Salmahat
 * @license MIT
 */

module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  rules: {
    query: $ => $.comparison,
    comparison: $ => seq($.identifier, '=', $.string),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
  }
});
