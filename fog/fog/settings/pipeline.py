# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

PIPELINE_JS = {
    'libs': {
        'source_filenames': (
            'jquery/jquery.js',
        ),
        'output_filename': 'libs.js',
    }
}

PIPELINE_COMPILER = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_DISABLE_WRAPPER = True

