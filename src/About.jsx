import React from 'react';

// Team profile picture import
import DChae from './images/squadpic/DC.png';
import Tigar from './images/squadpic/Tigar.png';
import Kesin from './images/squadpic/Kesin.png';
import ChooChoo from './images/squadpic/Chuchu.png';


function Profile (props) {
	return (
	<div id={props.id} class="squad">
		<div class={props.color} >
			<img src={props.img} class="picSquad" alt={props.name}/>
			<p class="nameBigger">{props.name}</p>
			<p class="basicFont">{props.job}</p>
			<p class="majorItalics">{props.major}</p>
			<p class="basicFont">{"Class of " + props.year}</p>
		</div>
	</div>)
}
function TeamProfiles(props) {
	return (
		<div id = "squadImages">
			<h1 id = "aboutSquad">Meet The Team</h1>
			<Profile id="TC" color="squadInfoB" img={Tigar} name="Tigar Cyr" job="Backend Developer & Team Manager" major="Computer Science BSE" year="2020"/>
			<Profile id="DC" color="squadInfoO" img={DChae} name="Daniel Chae" job="Full Stack Developer" major="Computer Science BSE" year="2020"/>
			<Profile id="KD" color="squadInfoB" img={Kesin} name="Kesin Ryan Dehejia" job="Frontend Developer" major="Computer Science BSE" year="2020"/>
			<Profile id="CC" color="squadInfoO" img={ChooChoo} name="Chris Chu" job="Frontend Developer" major="Civil and Environmental Engineering" year="2019"/>
		</div>
	)
}

function AboutInfo(props) {
	return (
		<div id = "aboutInfoDiv">
			<h1 id="aboutHeader">Room Draw Made Easy</h1>
			<p class="aboutInfo">
				Interact directly with rooms and buildings to find rooms on campus. 
				We emphasize simplicity and clean visualizations to help you find the perfect room for you.
			</p>
			<p class ="aboutInfo">
				Redraw is a final project for COS 333: Advanced Programming Techniques, 
				taught by Professor Brian Kernighan in Spring 2018. The team is advised by Jérémie Lumbroso. 
				Special acknowledgement for all who have helped us along the way.
			</p>
		</div>
	)
}

function AboutPage(props) {
	return (
		<div id = "aboutDiv">
			<AboutInfo/>
			<TeamProfiles/>
		</div>
	)
}

export default AboutPage;