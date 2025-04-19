export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-semibold">E-Commerce</h3>
            <p className="text-gray-400 text-sm">© 2025 All rights reserved</p>
          </div>
          
          <div className="flex gap-8">
            <div>
              <h4 className="font-medium mb-2">Quick Links</h4>
              <ul className="text-gray-400 text-sm">
                <li><a href="/products" className="hover:text-white">Products</a></li>
                <li><a href="/cart" className="hover:text-white">Cart</a></li>
                <li><a href="/auth" className="hover:text-white">Login</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Contact</h4>
              <ul className="text-gray-400 text-sm">
                <li>Email: contact@example.com</li>
                <li>Phone: (123) 456-7890</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}