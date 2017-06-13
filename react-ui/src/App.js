import React, {Component} from 'react';
import Request from 'superagent';
import _ from 'lodash';
import NavBar from './components/Navbar';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
          query: 'infinix',
        }
    }

    componentWillMount() {
        var query = this.state.query;
        var url = 'http://127.0.0.1:5000/search?q=' + query;
        Request.get(url).then((response) => {
            this.setState({products: response.body})
        });
    }

    getQuery(searchQuery) {
      this.setState({
        query: 'cubot'
      })
    }

    render() {
      var products = _.map(this.state.products, (products) => {
        return (
          <li className="col-xs-12 col-sm-8 col-md-3 col-lg-2">
            <div className="product">
              <img src={products.product_image} />
              <div className="product-store">
                { products.store == 'jumia' ? <img src="imgs/jumia.png" alt=""/> : <img src="http://image-s3.kilimall.co.ke/shop/common/05466175557864071.png" alt=""/>}
              </div>
              <div className="product-details">
                <h3>{products.name}</h3>
                <span>KSh {products.price}</span>
              </div>
              <div className="product-footer">
                <a href="">Buy Now</a>
                <a href="">Compare</a>
              </div>
            </div>
          </li>
        );
      });

      return (
            <div><NavBar />
                  <div className="app">

                    <ul className="row">{products}</ul>
                  </div>
            </div>
        );
    }
}

export default App;
