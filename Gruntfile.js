module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),


    less: {
      runningCause: {
        files: {
          'static/stylesheets/style.css': 'static/less/style.less',
        }
      }
    },

    copy: {
      runningCause: {
        files:[
        {
          cwd: 'node_modules/bootstrap/fonts',
          src:'**/*',
          dest: 'RunningCause/static/fonts',
          expand:true

        }
      ]  
      }
    }
  });

  

  // Load plugins here.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Register tasks here.
  grunt.registerTask('default', ['less', 'copy']);

};