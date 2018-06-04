import React from 'react';
import buildings from './json/buildings.json';

import name2Num from './json/name2num.json';

// Imports for AutoSuggestion
import DownshiftInput from './Downshift';
import { Form, Field } from 'react-final-form';


import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch';

import RoomCard from './RoomCard'

function BuildingSearch(props) {
    return (
        <div id="buildingNameSearch">
            <Field
              name="building"
              items={Object.values(buildings).map(building => {
                    return {value:building["name"]}
                })}
              component={DownshiftInput}
              placeholder="Search for Building..."
            />
        </div>
    )
}

function FloorSearch(props) {
    return (
        <div id="floorSearch">
            <label>Floor</label>
            <Field name="level" component="select" placeholder="#">
                <option />
                <option value="A">A</option>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
            </Field>
        </div>
    )
}

function DrawSearch(props) {
    return (
        <div id="drawSearch">
            <Field name="draw" component="select">
                <option />
                <option value="Butler">Butler</option>
                <option value="Forbes">Forbes</option>
                <option value="Independent">Independent</option>
                <option value="Mathey">Mathey</option>
                <option value="Rockefeller">Rockefeller</option>
                <option value="Upperclass">Upperclass</option>
                <option value="Whitman">Whitman</option>
                <option value="Wilson">Wilson</option>
            </Field>
        </div>
    )
}

function SizeSearch(props) {
    return (
        <div id="sizeSearch">
            <label>Minimum Size</label>
            <Field
              name="sqft__gte"
              component="input"
              type="number"
              min="0" 
              max="1150"
              placeholder="###"
            />
        </div>
    )
}

function SubmitButton(props) {
    return (
        <div id="divSubmitButton" className="buttons">
            <button
              id="submitButton" 
              type="submit"
              disabled={props.submitting || props.pristine}>
                <FontAwesomeIcon icon = {faSearch}/>
            </button>
        </div>
    )
}



/* validate: process the values returned when a form is submitted.
			If something is invalid, then return an error array. */
function formValidate(values) {
    var errArray = {};
    if (values.building) {
        let buildingName = values.building;
        if (buildingName.length > 30) {
            errArray.building = 'Name is too long';
        }
        else if (!name2Num.hasOwnProperty(buildingName)) {
            errArray.building = 'Does not exist';
        }
    }
    return errArray;
}



function Search(props) {return (
<div id="formBlock">
    <Form
      onSubmit={props.formSubmit}
      validate={formValidate}
      render={({ handleSubmit, pristine, submitting, values }) => (
        <form id="searchForm" onSubmit={handleSubmit}>
            <div id="buildingNameLabel">
                <label>
                    Building Name
                </label>
            </div>
            <BuildingSearch />  
            <FloorSearch />
            <div id="drawLabel">
                <label>
                    Draw Section
                </label>
            </div>
            <DrawSearch />
            <SizeSearch />
            <SubmitButton 
                submitting={submitting} 
                pristine={pristine}
            />
        </form>
      )}
    />
</div>
)}

function SearchResults(props) {
    return (
        <div>
            <p>{props.results.length + " Search Results"}</p>
            <ul id="roomSearchButtons">
                {props.results.map( room => 
                    <RoomCard 
                      room={room} 
                      getPolygons={props.getPolygons} 
                      updateFavorites={props.updateFavorites}
                      isFavorite={props.favoritesList.some(r => r.room_id === room.room_id)}
                    />
                    )}
            </ul>
            
            
        </div>
    )
}


export {Search, SearchResults};