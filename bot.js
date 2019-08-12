const http = require('http');
const url = require('url');
const mysql = require('mysql2/promise');
const mrequest = require('request-promise');
const bluebird = require('bluebird');

const DURATION = 1000 * 60 * 1;
const pool = mysql.createPool({
  host: '127.0.0.1',
  user: 'root',
  password: 'admin',
  database: 'mydb',
  port: 3308,
	waitForConnection: true,
	connectionLimit: 10,
	queueLimit: 0
});

var Authorization = '2114d9d47905e856521b5fdfb8faecd5d16c8928';
var querystring = require('querystring');
var postData = querystring.stringify({
  api_key: Authorization
});
const options = {
  hostname: '36.89.152.19',
  port: 8008,
  path: '/produksi-pi/produksi/index.php/tampilmerk',
  uri: 'http://36.89.152.19:8008/produksi-pi/produksi/index.php/tampilmasterdata',
  method: 'POST',
	body: postData,
  headers: {
  	'api_auth_key': Authorization,
    'Content-Type': 'application/x-www-form-urlencoded'
  }
};

postRequest = async function( opt, data ){
	return new Promise( function(resolve, reject){
		if( ! data ) data = postData;
			try {
			var request = http.request( opt, (res) => {
				var body = "";
				res.on('data', (d) => {
						body += d.toString();
					})
				res.on('end', () => {
						resolve(body);
					})
				});
			} catch(err) {
				console.log( '2',err);
				reject(err);
			}
			request.on('error', function(error) {
					console.log(error);
					reject(error);
				});
				request.write(data);
				request.end();
	});
}

asyncForEach = async function(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
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
			opt.old[doc] = JSON.parse( JSON.stringify(opt.old[doc]) );
			console.log(JSON.stringify(opt.old[doc]) , JSON.stringify(opt.new[doc]), (JSON.stringify(opt.old[doc]) != JSON.stringify(opt.new[doc])) );
			if( isObject( opt.old[doc] ) ) return JSON.stringify(opt.old[doc]) != JSON.stringify(opt.new[doc]) 
    	else return opt.old[doc] != opt.new[doc];
    }).map((doc)=>{ 
    	var obj = {};
    	obj[doc] = opt.new[doc];
    	return obj; 
    });
}

var checkSameObject = function( obj1, obj2 ){
	//console.log( JSON.stringify(obj1),  JSON.stringify(obj2));
	return JSON.stringify(obj1) == JSON.stringify(obj2);
}

var get = async function(pool, option){
	try {
		var [results, types] = await pool.query('SELECT * FROM `'+ option.table +'`', []);
		return results;
	} catch( err ) {
		return err;
	}
};

var update = async function(pool, option){
	try {
		var sql = 'UPDATE `'+ option.table +'` SET ';
		sql += option.data.map(function( obj ){
			return Object.keys(obj).map(function( head ){
				return " " + head + " = '" + obj[head] + "'";
			}).join(' , ');
		}).join('');
		sql += ' WHERE ';
		sql += option.where.map(function( obj ){
			return Object.keys(obj).map(function( head ){
				return " " + head + " = '" + obj[head] + "'";
			}).join(' AND ');
		}).join('');
		console.log(sql);
		var [results, types] = await pool.query(sql, []);
		return results;
	} catch( err ) {
		return err;
	}
}

var deletes = async function( pool, option ) {
	try {
		var sql = 'DELETE FROM `'+ option.table +'` WHERE ';
		sql += option.data.map(function( obj ){
			return Object.keys(obj).map(function( head ){
				return " " + head + " = '" + obj[head] + "'";
			}).join(' AND ');
		}).join('');
		console.log(sql);
		var [results, types] = await pool.query(sql, []);
		return results;
	} catch( err ) {
		return err;
	}
}

var insert = async function( pool, option ) {
	try {
		var sql = ' INSERT INTO '+ option.table +' (' + option.data.map(function( obj ){  console.log(obj); return Object.keys(obj).map(function(head){ return head; }); }).join(' , ') + ') ';
		sql += ' VALUES ( "' + option.data.map(function( obj ){ return Object.keys(obj).map(function(head){ return obj[head]; }).join('" , "'); }).join('')+ '" ) ';
		console.log(sql);
		var [results, types] = await pool.query(sql, []);
	} catch(err) {
		console.log(err);
		return err;
	}
}
/*
insert( '', {
	table: 'obat',
	data: [
		{ 'id_obat': 150, 'nama_obat': 'XX' }
	]
} );

update('', {
	table: 'obat',
	data: [
		{ 'id_obat': 150, 'nama_obat': 'XX' }
	]
});

deleteS('', {
	table: 'obat',
	data: [
		{ 'id_obat': 150, 'nama_obat': 'XX' }
	]
});
*/
var obat = async function(){
	try {
		var dataobat = await mrequest( options);
	} catch (error) {
		console.log(error);
	}
	if( dataobat ) {
		var objData = JSON.parse(dataobat);
		console.log(objData[0]);
		var objMasterObat = objData[0].obat.reduce(function( old, obat ) {
			old[ obat.id_obat ] = obat;
			return old;
		}, {});
		//console.log(objMasterObat);
		var [results, types] = await pool.query('SELECT * FROM `obat`', []);
		var objDBMasterObat = results.reduce(function( old, obj ){
			old[obj.id_obat] = obj;
			return old;
		}, {});
		//console.log(objDBMasterObat);
		if( checkSameObject( objMasterObat, objDBMasterObat) ) {
			console.log('same');
			setTimeout(obat, DURATION);
		} else {
			var arrNewData = getNewData( {new: objMasterObat, old: objDBMasterObat} );
			var arrRemoveData = getRemoveData( {new: objMasterObat, old: objDBMasterObat} );
			var arrNewObsoleteData = getReplaceObsoleteValue( {new: objMasterObat, old: objDBMasterObat} );
			await asyncForEach(arrNewObsoleteData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await update(pool, {table: 'obat', data: data, where: [{id_obat: Object.keys(newObj)[0] }]});
			});

			await asyncForEach(arrNewData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await insert(pool, {table: 'obat', data: data});
				console.log(' new ', res);
			});

			await asyncForEach(arrRemoveData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await deletes(pool, {table: 'obat', data: data});
				console.log(' remove ', res);
			});
			setTimeout(obat, DURATION);
		}
	}
};
obat();


var merk = async function(){
	try {
		options.uri ='http://36.89.152.19:8008/produksi-pi/produksi/index.php/tampilmerk';
		var data = await mrequest( options);
	} catch (error) {
		console.log(error);
	}
	if( data ) {
		var objData = JSON.parse(data);
		var objMasterObat = objData.reduce(function( old, obat ) {
			obat.id = obat.id * 1;
			old[ obat.id * 1 ] = obat;
			return old;
		}, {});
		//console.log(objMasterObat);
		var [results, types] = await pool.query('SELECT * FROM `merk`', []);
		var objDBMasterObat = results.reduce(function( old, obj ){
			old[obj.id * 1 ] = obj;
			return old;
		}, {});
		//console.log(objMasterObat, objDBMasterObat);
		
		if( checkSameObject( objMasterObat, objDBMasterObat) ) {
			console.log('merk same');
			setTimeout(merk, DURATION);
		} else {
			
			var arrNewData = getNewData( {new: objMasterObat, old: objDBMasterObat} );
			var arrRemoveData = getRemoveData( {new: objMasterObat, old: objDBMasterObat} );
			var arrNewObsoleteData = getReplaceObsoleteValue( {new: objMasterObat, old: objDBMasterObat} );
			await asyncForEach(arrNewObsoleteData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await update(pool, {table: 'merk', data: data, where: [{id: Object.keys(newObj)[0] }]});
				console.log('update',res);
			});
			

			await asyncForEach(arrNewData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await insert(pool, {table: 'merk', data: data});
				console.log(' new ', res);
			});

			await asyncForEach(arrRemoveData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await deletes(pool, {table: 'merk', data: data});
				console.log(' remove ', res);
			});
			setTimeout(merk, DURATION);
			
		}
	}
};
merk();


var komposisi = async function(){
	try {
		options.uri ='http://36.89.152.19:8008/produksi-pi/produksi/index.php/tampilkomposisi';
		var data = await mrequest( options);
	} catch (error) {
		console.log(error);
	}
	if( data ) {
		var objData = JSON.parse(data);
		//console.log(objData[0]);
		var objMasterObat = objData.reduce(function( olddata, komp ) {
			var obj = komp.komposisi.reduce(function( old, mat ){
				delete mat['nama_obat'];
				mat['id_merk'] = komp.id_merk;
				old[ komp.id_merk + '-' + mat.id_obat] = mat;
				return old;
			}, {});
			return Object.assign(olddata, obj);
		}, {});
		
		var [results, types] = await pool.query('SELECT * FROM `komposisi`', []);
		var objDBMasterObat = results.reduce(function( old, obj ){
			old[ obj.id_merk + '-' + obj.id_obat] = obj;
			return old;
		}, {});
		//console.log(objMasterObat, objDBMasterObat);
		
		if( isEqual( objMasterObat, objDBMasterObat) ) {
			console.log('komposisi same');
			setTimeout(komposisi, DURATION);
		} else {
			console.log('komposisi not same');
			var arrNewData = getNewData( {new: objMasterObat, old: objDBMasterObat} );
			var arrRemoveData = getRemoveData( {new: objMasterObat, old: objDBMasterObat} );
			var arrNewObsoleteData = getReplaceObsoleteValue( {new: objMasterObat, old: objDBMasterObat} );
			
			
			await asyncForEach(arrNewObsoleteData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await update(pool, {table: 'komposisi', data: data, where: [{id_merk: data[0]['id_merk'], id_obat: data[0]['id_obat'] }] });
				console.log('update',res);
			});
			

			await asyncForEach(arrNewData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await insert(pool, {table: 'komposisi', data: data});
				console.log(' new ', res);
			});
			
			await asyncForEach(arrRemoveData, async (newObj) => {
				var data = Object.keys(newObj).map(( doc )=>{return newObj[doc] });
				var res = await deletes(pool, {table: 'komposisi', data: data});
				console.log(' remove ', res);
			});
			setTimeout(komposisi, DURATION);
		}		
	}
};
komposisi();

var insert_timbang = async function(){
	var [results, types] = await pool.query('SELECT * FROM `hasil` WHERE NOT jam_timbang = "null" LIMIT 1', []);
	var objTimbang = results.map(function( obj ){
		return {
			jumlah_berat: obj.netto,
		  	waktu: obj.jam_timbang,
		  	id_merk: obj.id_merk,
		  	id_obat: obj.id_material
		};
	});
	await asyncForEach(objTimbang, async (newObj) => {
		newObj.api_key = Authorization;
		var postData = querystring.stringify(newObj);
		options.body = postData;
		try {
			options.uri ='http://36.89.152.19:8008/produksi-pi/produksi/index.php/timbangan/add';
			var data = await mrequest( options);
		} catch (error) {
			console.log(error);
		}
		var objResult = JSON.parse(data);
		
		if( objResult.status == "200" ) {
			update(pool, {
				table: 'hasil',
				data: [
					{ 'jam_timbang': null }
				],
				where: [
					{ 'jam_timbang': newObj.waktu }
				] 
			});	
			setTimeout(insert_timbang, DURATION);
		} else {
			console.log(data);
			setTimeout(insert_timbang, DURATION);
		}
	});
}
insert_timbang();

var isEqual = function (value, other) {
	// Get the value type
	var type = Object.prototype.toString.call(value);
	// If the two objects are not the same type, return false
	if (type !== Object.prototype.toString.call(other)) return false;
	// If items are not an object or array, return false
	if (['[object Array]', '[object Object]'].indexOf(type) < 0) return false;
	// Compare the length of the length of the two items
	var valueLen = type === '[object Array]' ? value.length : Object.keys(value).length;
	var otherLen = type === '[object Array]' ? other.length : Object.keys(other).length;
	if (valueLen !== otherLen) return false;
	// Compare two items
	var compare = function (item1, item2) {
		// Get the object type
		var itemType = Object.prototype.toString.call(item1);
		// If an object or array, compare ecursively
		if (['[object Array]', '[object Object]'].indexOf(itemType) >= 0) {
			if (!isEqual(item1, item2)) return false;
		}
		// Otherwise, do a simple comparison
		else {
			// If the two items are not the same type, return false
			if (itemType !== Object.prototype.toString.call(item2)) return false;
			// Else if it's a function, convert to a string and compare
			// Otherwise, just compare
			if (itemType === '[object Function]') {
				if (item1.toString() !== item2.toString()) return false;
			} else {
				if (item1 !== item2) return false;
			}
		}
	};
	// Compare properties
	if (type === '[object Array]') {
		for (var i = 0; i < valueLen; i++) {
			if (compare(value[i], other[i]) === false) return false;
		}
	} else {
		for (var key in value) {
			if (value.hasOwnProperty(key)) {
				if (compare(value[key], other[key]) === false) return false;
			}
		}
	}
	// If nothing failed, return true
	return true;
};

