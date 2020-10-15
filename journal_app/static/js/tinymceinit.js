tinymce.init({
    selector: '#tinymceid',
    plugins: 'wordcount emoticons lists',
    skin: 'oxide-dark',
    menubar:false,
    toolbar: 'undo redo | underline strikethrough bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | emoticons',
    style_formats: [
        { title: 'Entry', block: 'p'},
    ]
});
