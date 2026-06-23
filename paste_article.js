const article = require('fs').readFileSync('C:/Users/69547/.openclawcn/workspace/shunshou/article.md', 'utf8');
const cm = document.querySelector('.CodeMirror').CodeMirror;
cm.setValue(article);
'article set: ' + article.length + ' chars';