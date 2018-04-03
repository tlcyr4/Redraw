import React, { Component } from 'react';
import './Image1.css'
import Test1 from './Brown/0014-01.png';

class Image1 extends Component {
	render() {
		return (
			<div className = "testImage">
				<img src = {Test1} className = "Image1" />
			</div>
		)
	}
} 

export default Image1;