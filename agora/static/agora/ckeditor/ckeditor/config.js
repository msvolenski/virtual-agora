/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	config.extraPlugins = 'image2';
      
    
	config.language = 'pt-br';

      config.toolbar = 'MyToolbar';

        config.toolbar_MyToolbar =
        [
            
        ];
    
        config.toolbar_Basic =
        [
            ['Bold', 'Italic', '-', 'NumberedList', 'BulletedList', '-', 'Link', 'Unlink','-','About']
        ];


        config.width = '100%'






	// config.uiColor = '#AADC6E';
};

