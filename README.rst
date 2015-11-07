Assets in Django with gulp as a pipeline
========================================

This is the approach we use on Opbeat.com. In gulp it uses the
```gulp-asset-manifest```_ module. In Django, it uses custom template
tags to load the manifest.

We use it for JS and CSS, in this example it’s some JS library files.

gulpfile.js
-----------

::

    gulp.task('prepare-scripts', function() {
       gulp.src('static/js/libs/*.js')
            .pipe(concat('libs.min.js'))
            .pipe(uglify())
            .pipe(rev())
            .pipe(assetManifest({
                bundleName: 'lib_js',
                manifestFile: 'assets/asset_manifest.json',
                log: true,
                pathPrepend: CACHED_DIR
            }))
            .pipe(gulp.dest(CACHED_DIR));
    });

asset\_manifest.json
====================

::

    {
        "lib_js": [
            "static/build/cached/libs.min-69896a86.js"
        ],
    }

template.html
=============

::

    {% load assets_url %}

    {% do_asset "lib_js" %}
        <script type="text/javascript" src="{{ ASSET_URL }}" charset="utf-8" crossorigin></script>
    {% end_do_assets %}

result.html
===========

::

    <script type="text/javascript" src="/static/build/cached/libs.min-69896a86.js" charset="utf-8" crossorigin></script>

.. _``gulp-asset-manifest``: https://github.com/vanjacosic/gulp-asset-manifest
