import React, {Component} from 'react';
import _ from 'lodash';

class NavBar extends Component {
    render() {
        return (
            <div className="navbar">
              <div className="search-form">
                <input type="text" placeholder="Search product"/>
              </div>
            </div>
        );
    }
}

export default NavBar;
