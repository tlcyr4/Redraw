import React, { Component } from 'react'
import Background from './Colleges2009.png';
import './Home.css';

class Home extends Component {
	render () {
		return (
			<div>
				<img src = {Background} className = "background" alt = "bg"/>
			</div>
		);
	}
}

export default Home; 
