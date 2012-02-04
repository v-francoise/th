CKEDITOR.editorConfig = function( config )
{
 // Define changes to default configuration here. For example:
 // config.language = 'fr';
 // config.uiColor = '#AADC6E';

  config.toolbar = 'MyToolbar';
  config.language = 'fr';
  config.toolbar_MyToolbar =
  [
   ['Save','Print','Preview','NewPage','-'],
   ['Maximize'],
   ['SelectAll','Cut','Copy','Paste','PasteText','-','ShowBlocks'],
   '/',
   ['Source','-','UIColor','-','Undo','Redo','-'],
   '/',
   ['NumberedList','BulletedList','-'],
   ['Indent','Outdent'],
   ['Bold','Italic','Underline','Strike','-'],
   ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
   ['TextColor','BGColor','RemoveFormat'],
   ['Styles','Font','FontSize'],
   ['Subscript','Superscript'],
   ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar'],
   ['Link','Unlink']
  ];

};
};