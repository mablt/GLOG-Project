
//TODO Make the header !!!!!!!!!!!!


/** 
* Add the protein data to the webpage.
* @param {Object} protein_data - Protein data object from backend.
*/
function addProteinDataToWebpage(protein_data){
    $("#prediction-3d-div_src").html(protein_data["pdb"]);
    $("#protein-name").html(protein_data["name"]);
    $("#organism").html(protein_data["species"]);
    $("#gene-name").html(protein_data["gene"]);
    $("#protein-id").html(protein_data["id"]);
    $("#protein-length").html(protein_data["length"]);
    // 3D visualisation with GLmol integration
    add3DPrediction();
    add2DPrediction(protein_data["2D_prediction"]);
}


/** 
* Add the 3D prediction to the webpage.
*/
function add3DPrediction(){
    var prediction_3d = new GLmol("prediction-3d-div", true);
    prediction_3d.loadMolecule();
}


/** 
* Add the 2D prediction figure to the webpage.
* @param {String} encodedFigure - String which represant the encoded figure.
*/
function add2DPrediction(encodedFigure){
    $("#prediction-2d-figure").html("<img src='data:image/png;base64,"+encodedFigure+"''>");
    $("#prediction-2d-legend").html("<img src='/static/img/legend.png'>");
}


/** 
* Add links of the  3 better Blast hits of the blast done executed in backend.
*/
function addBlastData(){
    $("#results-actions").html('<p>Le blast est en cours ...</p>')
    $.post('/'+$("#protein-id").text()+'/blast').done(function(blast_ids){
        var data = "IDs des 3 protéines ayant la meilleure e-value : <br>";
        blast_ids.forEach(id => {
            data += "<a href='https://www.rcsb.org/structure/"+id+"' target='_blank'>"+id+"</a> <br>"
        });
        $("#results-actions").html(data);
    }).fail( function(){
        $("#results-actions").html("<p>Le blast n'a pas fonctionné !</p>")
    });
}

/** 
* Add ramachandran figure generated in backend to the webpage.
*/
function addRamachandranData(){
    $("#results-actions").html('<p>Le ramachandran est en cours ...</p>')
            $.post('/'+$("#protein-id").text()+'/ramachandran').done(function(response){
                var data = "<img src='data:image/png;base64,"+response+"''>"
                $("#results-actions").html(data);
            }).fail( function(){
                $("#results-actions").html("<p>Le ramachandran n'a pas fonctionné !</p>")
            });
}



// Proteins buttons onclick event management
var proteinsButtons = document.querySelectorAll('#dpdwn');
for (var i=0 ; i < proteinsButtons.length ; i++){
    proteinsButtons[i].onclick = function(){
        // Clear data presents on the webpage
        $("#prediction-3d-div").empty();
        $("#results-actions").empty();
        $("#prediction-2d-figure").empty();
        $("#prediction-2d-legend").empty();
        $.post('/'+this.value).done(function(protein_data){
            addProteinDataToWebpage(protein_data);
            
        })
    };
};

// Functionalities buttons onclick event management
var functionalitiesButtons = document.querySelectorAll("#actions-button");
for (var i=0 ; i < functionalitiesButtons.length ; i++){
    functionalitiesButtons[i].onclick = function(){
        // Clear functionalities data panel 
        $("#results-actions").empty();
        // Add data
        if(this.value == "blast"){
            addBlastData();
        }
        else if(this.value == "ramachandran"){
            addRamachandranData();
        }
        
    };
};