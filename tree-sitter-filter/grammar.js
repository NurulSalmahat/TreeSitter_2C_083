/**
 * @file A simple filter query language for searching and filtering data.
 * @author Nurul Salmahat
 * @license MIT
 */

module.exports = grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,
  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,
      $.and_expression,
    ),

    comparison: $ => seq(
      $.identifier,
      choice('=', '!=', '>', '<', '>=', '<='),
      $._value,
    ),

    and_expression: $ => prec.left(seq($._expr, 'and', $._expr)),

    _value: $ => choice($.string, $.number),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
  }
});
