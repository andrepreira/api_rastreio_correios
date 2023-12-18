(function () {
    var Contrast = {
        storage: 'contrastState',
        cssClass: 'contrast',
        currentState: null,
        check: checkContrast,
        getState: getContrastState,
        setState: setContrastState,
        toogle: toogleContrast,
        updateView: updateViewContrast
    };

    window.toggleContrast = function () { Contrast.toogle(); };

    Contrast.check();

    function checkContrast() {
        this.updateView();
    }

    function getContrastState() {
        return localStorage.getItem(this.storage) === 'true';
    }

    function setContrastState(state) {
        localStorage.setItem(this.storage, '' + state);
        this.currentState = state;
        this.updateView();
    }

    function updateViewContrast() {
        var body = document.body;
        var span = document.querySelector('#tooltip-vermais');

        if (this.currentState === null)
            this.currentState = this.getState();

        if (this.currentState){
            body.classList.add(this.cssClass);
            //
            if(span !== null){
                span.classList.remove('title');
                span.classList.add('title-c');
            }
        
        } else {
            body.classList.remove(this.cssClass);
            //
            if(span !== null){
                span.classList.remove('title-c');
                span.classList.add('title');
            }
        }

    }

    function toogleContrast() {
        this.setState(!this.currentState);
    }
})();