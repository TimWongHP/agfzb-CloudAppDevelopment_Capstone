const Cloudant = require('@cloudant/cloudant'); 

function main(params) {
    return new Promise(function (resolve, reject) {
        
        const cloudant = Cloudant({
            url: params.COUCH_URL,
            plugins: {iamauth: {iamApiKey:params.IAM_API_KEY}} 
        });
        const dealershipDb = cloudant.use('dealerships'); 
        if (params.state) { 
            // return dealerships for the specified state (if specified)
            dealershipDb.find({"selector": {"st": {"$eq": params.state}}}, 
                function (err, result) { 
                        if (err) { 
                            console.log(err) 
                            reject(err); 
                        } 
                        let code=200; 
                            if (result.docs.length==0) { 
                                code= 404; 
                            }
                        resolve({ 
                            statusCode: code, 
                            headers: {'Content-Type': 'application/json'}, 
                            body: result 
                        }); 
                    }); 
        } else { 
            // return all documents if no parameters are specified
            dealershipDb.list(
                { include_docs: true }, 
                function (err, result) { 
                    if (err) { 
                        console.log(err) 
                        reject(err); 
                    } 
                    resolve({ 
                        statusCode: 200, 
                        headers: { 'Content-Type': 'application/json' }, 
                        body: result 
                    }); 
                }
            ); 
        } 
    });
}

function main(params) {
    if(params.statusCode && params.statusCode === 200){
        if(params.body.docs){
            const res = params.body.docs.map((doc) => {
                return{
                 id: doc.id,
                 city: doc.city,
                 state: doc.state,
                 st: doc.st,
                 address: doc.address,
                 zip: doc.zip,
                 lat: doc.lat,
                 long: doc.long,
            }});
           return {listOfDealership: res};
        }else{
            const res = params.body.rows.map((row) => {
                return{
                 id: row.doc.id,
                 city: row.doc.city,
                 state: row.doc.state,
                 st: row.doc.st,
                 address: row.doc.address,
                 zip: row.doc.zip,
                 lat: row.doc.lat,
                 long: row.doc.long,
            }});
           return {listOfDealership: res};
        }
    }
    else{
        return {
            statusCode: params.statusCode, 
            message: "Error"
        }
    }
 }
