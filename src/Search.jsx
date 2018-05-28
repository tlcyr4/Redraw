import React from 'react';
import buildings from './json/buildings.json';

// Imports for AutoSuggestion
import DownshiftInput from './Downshift';
import { Form, Field } from 'react-final-form';


import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faSearch from '@fortawesome/fontawesome-free-solid/faSearch';

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

function Search(props) {return (
<div id="formBlock">
    <Form
      onSubmit={props.formSubmit}
      validate={props.formValidate}
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
            <ul id="roomSearchButtons">
                {props.results.map( r => 
                    <li>
                        <input 
                            id={r['room_id']}
                            bldg={r['building_name']}
                            level={r['level']}
                            type="button"
                            value={r['building_name'] + " " + r['number']}
                            onClick={ (e) => props.handleFloorplanSwitch(e) }
                        />
                    </li>
                    )}
            </ul>
            <p>{props.results.length + " Results Found"}</p>
        </div>
    )
}


export {Search, SearchResults};