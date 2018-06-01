import React from 'react';


// Expansion panel section
import ExpansionPanel, {
	ExpansionPanelSummary,
	ExpansionPanelDetails,
} from 'material-ui/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Typography from 'material-ui/Typography';

function Favorites(props) {
    return (
<ExpansionPanel 
    className = "expPanel" 
    defaultExpanded={true}>
    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
        <Typography variant="subheading">Favorites</Typography>
    </ExpansionPanelSummary>
    <ul id="favoriteButtons">
        {props.favoritesList.map((room, index)=>(
            <li>
            <ExpansionPanelDetails>
                <input
                  id={room.room_id}
                  level={room.level}
                  bldg={room.building_name}
                  onClick={e => props.handleFloorplanSwitch(e)}
                  type="button"
                  value = {room.building_name + " " + room.number}/> 
            </ExpansionPanelDetails>
            </li>
        ))}
    </ul>
</ExpansionPanel>
    )
}


export default Favorites;
