var gulp = require('gulp');
var sass = require('gulp-sass');
var prefix = require('gulp-autoprefixer');
var minify = require('gulp-clean-css');
var plumber = require('gulp-plumber');

function onError(err) {
    console.log(err);
}

gulp.task('sass', function(){
    return gulp.src('static/css/*.scss')
        .pipe(sass())
        .pipe(prefix('last 2 versions'))
        .pipe(minify())
        .pipe(gulp.dest('static/css/'))
        .pipe(plumber({
            errorHandler: onError
        }))
});


gulp.task('watch', function() {
  gulp.watch('static/css/*.scss', gulp.series('sass'));
});
