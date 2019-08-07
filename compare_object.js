var log = function(text){
	document.write('<p>' +text + '</p>');
}
var objOld = {
	142: 'AAS',
    143: 'CCN',
    231: {tes:123}
};
var objNew = {
    143: 'CCN',
    231: {tes:223},
    145: 'XXC'
}
function isObject (value) {
	return value && typeof value === 'object' && value.constructor === Object;
}
var getNewData = function( opt ){
	return Object.keys(opt.new).filter((doc)=>{
    	return !(doc in opt.old);
    }).map((doc)=>{ 
    	var obj = {};
    	obj[doc] = opt.new[doc];
    	return obj; 
    });
};
var getRemoveData = function( opt ){
	return Object.keys(opt.old).filter((doc)=>{
    	return !(doc in opt.new);
    }).map((doc)=>{ 
    	var obj = {};
    	obj[doc] = opt.old[doc];
    	return obj; 
    });
};
var getReplaceObsoleteValue = function(opt) {
	return Object.keys(opt.old).filter((doc)=>{
    	return (doc in opt.new);
    }).filter(function( doc ){
    	if( isObject( opt.old[doc] ) ) return JSON.stringify(opt.old[doc]) != JSON.stringify(opt.new[doc]) 
    	else return opt.old[doc] != opt.new[doc];
    }).map((doc)=>{ 
    	var obj = {};
    	obj[doc] = opt.new[doc];
    	return obj; 
    });
}
var res = JSON.stringify(objNew) == JSON.stringify(objOld)
if( !res ) {
	var newData = getReplaceObsoleteValue({
    	new: objNew,
        old: objOld
    });
	log(JSON.stringify(newData));
}


//source: https://webbjocke.com/javascript-check-data-types/
