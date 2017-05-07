import React, {Component} from 'react';
import Request from 'superagent';
import _ from 'lodash';

class NavBar extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    componentWillMount() {

    }

    render() {
        return (
            <div className="navbar">
              <div className="search-form">
                <input type="text" placeholder="Search product"/>
                <input type="submit" value="Search"/>
              </div>
            </div>
        );
    }
}

export default NavBar;
