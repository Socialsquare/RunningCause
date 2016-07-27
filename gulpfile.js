// var gulp = require('gulp');
// var autoprefixer = require('gulp-autoprefixer');
// var concat = require('gulp-concat');
// var del = require('del');
// var livereload = require('gulp-livereload');
// var minify = require('gulp-minify');
// var minifycss = require('gulp-minify-css');
// var plumber = require('gulp-plumber');
// var rename = require('gulp-rename');
// var runSequence = require('run-sequence');
// var sass = require('gulp-sass');
// var svgmin = require('gulp-svgmin');
// var svgstore = require('gulp-svgstore');
// var watch = require('gulp-watch');
//
//
// // 2. FILE PATHS
// // - - - - - - - - - - - - - - -
//
// var paths = {
//   static: [
//     'assets/static/'
//   ],
//   sass: [
//     'src/css/base.scss'
//   ],
//   sassWatch: [
//     'src/css/**/*.scss',
//   ],
//   js: [
//     'node_modules/svg4everybody/dist/svg4everybody.js',
//     'src/js/*.js'
//   ],
//   svg: [
//     'src/img/*.svg'
//   ]
// }
//
// // 3. TASKS
// // - - - - - - - - - - - - - - -
//
// // Cleans the build directory
// gulp.task('clean', function() {
//   return del(paths.static + '*');
// })
//
// // Compiles Sass
// gulp.task('sass', function() {
//   return gulp.src(paths.sass)
//     .pipe(plumber({
//       errorHandler: function(err) {
//         console.log(err);
//         this.emit('end');
//       }
//     }))
//     .pipe(sass())
//     .pipe(autoprefixer({
//       browsers: ['last 4 versions', 'ie 10']
//     }))
//     .pipe(gulp.dest('.tmp/css'))
//     .pipe(rename({
//       suffix: '.min'
//     }))
//     .pipe(minifycss())
//     .pipe(gulp.dest(paths.static + ''));
// });
//
// // Compiles JS
// gulp.task('js', function() {
//   return gulp.src(paths.js)
//     .pipe(plumber({
//       errorHandler: function(err) {
//         console.log(err);
//         this.emit('end');
//       }
//     }))
//     .pipe(concat('base.js'))
//     .pipe(gulp.dest(paths.static + ''))
//     .pipe(rename('base.js'))
//     .pipe(minify())
//     .pipe(gulp.dest(paths.static + ''));
//     });
//
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
// gulp.task('watch', function() {
//   // Watch Sass
//   gulp.watch(paths.sassWatch, ['sass']);
//
//   // Watch javascript
//   gulp.watch(paths.js, ['js']);
//
//   // Watch svg
//   gulp.watch(paths.svg, ['svg-sprite']);
//
// });
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
