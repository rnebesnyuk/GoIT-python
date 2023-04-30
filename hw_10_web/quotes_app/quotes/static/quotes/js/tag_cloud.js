var tagLinks = document.querySelectorAll('#tags-container .tag');
var minFontSize = 12;
for (var i = 0; i < tagLinks.length; i++) {
    var fontSize = 28 - i * 2 / tagLinks.length;
    if (fontSize < minFontSize) {
        fontSize = minFontSize;
    }
    var tagElement = tagLinks[i];
    tagElement.classList.add('tag');
    tagElement.style.fontSize = fontSize + 'px';
    tagElement.href = '/tag/tag-' + i;
    tagElement.textContent = 'Tag ' + i;
    tagLinks[i].style.fontSize = fontSize + 'px';
}
