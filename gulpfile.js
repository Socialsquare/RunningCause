var gulp = require('gulp');
var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var del = require('del');
// var livereload = require('gulp-livereload');
var uglify = require('gulp-uglify');
var cleancss = require('gulp-clean-css');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var runSequence = require('run-sequence');
var sass = require('gulp-sass');
// var svgmin = require('gulp-svgmin');
// var svgstore = require('gulp-svgstore');
// var watch = require('gulp-watch');
//
//
// 2. FILE PATHS
// - - - - - - - - - - - - - - -

var staticDir = 'RunningCause/static/'

var paths = {
  css: [
    staticDir + 'css/'
  ],
  js: [
    staticDir + 'js/'
  ]
}

var files = {
  static: [
    staticDir
  ],
  sass: [
    paths.css + '*.scss'
  ],
  sassWatch: [
    paths.css + '**/*.scss'
  ],
  js: [
    'node_modules/bootstrap/dist/js/bootstrap.min.js'
    // 'node_modules/svg4everybody/dist/svg4everybody.js',
    // 'src/js/*.js'
  ],
  jsWatch: [
    paths.js + '*.js'
  ],
  svg: [
    'src/img/*.svg'
  ]
}
//
// // 3. TASKS
// // - - - - - - - - - - - - - - -

// Cleanup
// gulp.task('cleanup', function() {
//   return del(paths.js + 'main.js');
// })

// Compiles Sass
gulp.task('sass', function() {
  return gulp.src(files.sass)
    .pipe(plumber({
      errorHandler: function(err) {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(sass())
    .pipe(autoprefixer({
      browsers: ['last 4 versions', 'ie 10']
    }))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(cleancss())
    .pipe(gulp.dest(paths.css + ''));
});

// Compiles JS
gulp.task('js', function() {
  return gulp.src(files.js)
    .pipe(plumber({
      errorHandler: function(err) {
        console.log(err);
        this.emit('end');
      }
    }))
    .pipe(concat('main.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(paths.js + ''));
});

// // Create SVG sprite
// gulp.task('svg-sprite', function() {
//   return gulp.src(paths.svg)
//     .pipe(plumber({
//       errorHandler: function(err) {
//         console.log(err);
//         this.emit('end');
//       }
//     }))
//     .pipe(svgmin())
//     .pipe(rename({
//       prefix: 'sprite_'
//     }))
//     .pipe(svgstore())
//     .pipe(rename('sprite.svg'))
//     .pipe(gulp.dest(paths.static + ''));
//     });
//
//
gulp.task('watch', function() {
  gulp.watch(files.sassWatch, ['sass']);
  gulp.watch(files.jsWatch, ['js']);

  // Watch svg
  // gulp.watch(paths.svg, ['svg-sprite']);
});


//
// // Builds your entire app once, without starting a server
// gulp.task('build', function(callback) {
//   runSequence(
//     'clean', ['sass', 'js', 'svg-sprite'],
//     callback);
// });
//
// // Default task: builds your app, starts a server, and recompiles assets when they change
// gulp.task('default', function(callback) {
//   runSequence(
//     'clean', ['sass', 'js', 'svg-sprite'],
//     'watch',
//     callback);
// });


// Default task: builds your app, starts a server, and recompiles assets when they change
gulp.task('default', function(callback) {
  runSequence(
    // 'clean',
    ['sass', 'js'],
    'watch',
    callback);
});
