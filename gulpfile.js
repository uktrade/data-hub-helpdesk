'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const del = require('del');

const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/frontend/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/helpdesk/helpdesk/static/css`;
const CSS_FILES = `${CSS_DIR}/**/*.css`;
const CSS_MAPS = `${CSS_DIR}/**/*.css.map`;
const GOVUK_ASSETS_PATH = `${PROJECT_DIR}/node_modules/govuk-frontend/assets`;

gulp.task('clean', function() {
  return del([CSS_FILES, CSS_MAPS]);
});

gulp.task('copy', function() {
  return gulp
    .src([`${GOVUK_ASSETS_PATH}/**/*`], { base: GOVUK_ASSETS_PATH })
    .pipe(gulp.dest('/tmp'));
});

gulp.task('sass:compile', function() {
  return gulp
    .src(SASS_FILES)
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        includePaths: ['./conf/'],
        outputStyle: 'compressed'
      }).on('error', sass.logError)
    )
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(CSS_DIR));
});

gulp.task('sass:watch', function() {
  gulp.watch([SASS_FILES], gulp.series('sass:compile'));
});

gulp.task('sass', gulp.series('clean', 'sass:compile'));

gulp.task('default', gulp.series('sass'));


