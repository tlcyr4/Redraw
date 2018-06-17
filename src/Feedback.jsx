import React from 'react';

// has the same styling as the content in About page, therefore reusing the id names
function FeedbackPage(props) {
	return (
		<div id = "aboutDiv">
			<div id = "aboutInfoDiv">
				<h1 id = "aboutHeader">Feedback</h1>
				<p class = "aboutInfo">
					We value any feedback you give to us, as we are always trying to improve.
				</p>
				<p class = "aboutInfo">
					Please send an email to <a href="mailto:tcyr@princeton.edu">the team</a> with your feedback and we will 
					be sure to get back to you, as needed!
				</p>
				<p class = "aboutInfo">
					Or take <a href="https://goo.gl/forms/2dHxJSRLhcgi2wjM2">this survey</a> to give us an evaluation of the site!
						We take your input very seriously and are always striving to improve the site.
				</p>
				<p class = "aboutInfo">
					Thank you!
				</p>
				<p class = "aboutInfo">
					~ Redraw Team
				</p>

			</div>
		</div>
	)
}

export default FeedbackPage;