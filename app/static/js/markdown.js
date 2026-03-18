
function render() {
  document.querySelectorAll(".markdown").forEach(elem => {
    let md = elem.textContent;
    elem.textContent = ""

    md = md.replace(/^###### (.*$)/gim, "<h6>$1</h6>");
    md = md.replace(/^##### (.*$)/gim, "<h5>$1</h5>");
    md = md.replace(/^#### (.*$)/gim, "<h4>$1</h4>");
    md = md.replace(/^### (.*$)/gim, "<h3>$1</h3>");
    md = md.replace(/^## (.*$)/gim, "<h2>$1</h2>");
    md = md.replace(/^# (.*$)/gim, "<h1>$1</h1>");

    md = md.replace(/\*\*(.*?)\*\*/gim, "<b>$1</b>");
    md = md.replace(/\*(.*?)\*/gim, "<i>$1</i>");
    md = md.replace(/\[(.*?)\]\((.*?)\)/gim, `<a href="$2">$1</a>`);

    md = md.replace(/\n/g, "<br>");

    elem.innerHTML = md;
  });
}