if (!window.dash_clientside) { window.dash_clientside = {}; }
window.dash_clientside.clientside = {
    // update_timer: function (value) {
    //     return new Date().toUTCString();
    // },
    difftime: function (val,start,pas){
        // console.log(typeof start)
        if(typeof start === 'number'){
            // console.log('pass')
             var ts = (new Date()).getTime()/1000-start;
             return new Date((ts+pas['time']) * 1000).toISOString().substr(11, 10)
        }
        else{
            //console.log(new Date(pas['time'] * 1000).toISOString().substr(11, 8))
            return new Date(pas['time'] * 1000).toISOString().substr(11, 10)
        }
    }
}