javascript:(function(){location.reload();var i=document.createElement('iframe');document.body.appendChild(i);prompt('Here is your token',i.contentWindow.localStorage.token.replace(/"/g,''));})();
