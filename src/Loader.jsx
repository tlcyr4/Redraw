import React from 'react';


import { RingLoader } from 'react-spinners';

function Loader(props) {
	return (
		<div id="loading">
			<RingLoader
				color={'#ffa500'} 
				loading={props.loading} 
			/>
		</div>
	)
}

export default Loader;