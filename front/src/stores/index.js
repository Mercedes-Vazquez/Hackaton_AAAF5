// require all files in dir

var context = require.context(".", true, /\.js$/);
context.keys().forEach(function (key) {
  context(key);
});
