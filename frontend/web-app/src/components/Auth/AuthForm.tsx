import React, {useState} from 'react';


const AuthForm = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username:'',
        email:'',
        password:''
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };
    const validateForm = () => {
        if (!formData.username.trim()) return 'Username is required';
        if (!formData.email.trim()) return 'Email is required';
        if (!formData.password.trim()) return 'Password is required';
        if (formData.password.length < 6) return 'Password must be at least 6 characters';
        return null;
    };
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess('');

        try{
            const endpoint = isLogin ? '/api/auth/login' : 'api/auth/signup';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();

            if (response.ok) {
                setSuccess (isLogin ? 'Login successfull!' : 'Account created successfully!')
            } else {
                setError(data.message || 'something went wrong');
            }
        }
        catch (err){
            setError('Network error. Please try again');
        }finally {
            setIsLoading(false);
        }
        
        console.log('Form data: ', formData);
        console.log('Mode:', isLogin? 'login': 'signup');
    };

    return (
        <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-lg shadow-md">
            <form onSubmit={handleSubmit} className="space-y-4">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6"> 
                    {isLogin ? 'Login' : 'Signup'}
                </h2>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button 
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                >
                    {isLogin ? 'Login' : 'Signup'}
                </button>

                <button type="button" 
                    onClick={() => setIsLogin(!isLogin)}
                    className="w-full bg-transparent text-blue-500 py-2 px-4 rounded-md border border-blue-500 hover:bg-blue-50 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                
                >
                    {isLogin ? 'Need an account? Signup' : 'Have an account? Login'}
                </button>
            
                    
            </form>
        </div>
    )
}

export default AuthForm;

