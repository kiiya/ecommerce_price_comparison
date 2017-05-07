import React, {Component} from 'react';
import Request from 'superagent';
import _ from 'lodash';
import NavBar from './components/Navbar';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    componentWillMount() {
        var query = 'iphone 6s 64gb';
        var url = 'http://127.0.0.1:5000/search?q=' + query;
        Request.get(url).then((response) => {
            this.setState({products: response.body})
        });
    }

    render() {
        console.log("Products: ", this.state.products);

        var products = _.map(this.state.products, (products) => {
            return (
              <li>
                <div className="product">
                  <div className="product-store">
                    { products.store == 'jumia' ? <img src="imgs/jumia.png" /> : <img src="http://image-s3.kilimall.co.ke/shop/common/05466175557864071.png" /> }
                  </div>
                  <div className="product-image">
                    <a href={ products.product_url }><img src={products.product_image} alt="something"/></a>
                  </div>
                  <div className="product-details">
                    <h3>{ products.name }</h3>
                    <span>KSh { products.price }</span>
                  </div>
                  <div className="product-footer">
                    <a>Buy Now</a>
                  </div>
                </div>
              </li>
            )
        });

        return (
            <div className="App">
                  <NavBar />
                  <ul>{products}</ul>
            </div>
        );
    }
}

export default App;
