import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="text-center py-12 bg-gray-50 rounded-lg">
        <h1 className="text-4xl font-bold mb-4">Welcome to Our E-Commerce Store</h1>
        <p className="text-xl text-gray-600 mb-8">Discover amazing products at great prices</p>
        <Link to="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 inline-block">
          Shop Now
        </Link>
      </section>
      
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Wide Selection</h3>
          <p className="text-gray-600">Browse through our extensive collection of products</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Fast Delivery</h3>
          <p className="text-gray-600">Get your orders delivered quickly and securely</p>
        </div>
        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-semibold mb-2">Best Prices</h3>
          <p className="text-gray-600">Enjoy competitive prices and regular discounts</p>
        </div>
      </section>
    </div>
  );
}