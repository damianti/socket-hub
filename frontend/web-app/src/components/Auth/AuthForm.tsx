import React, {useState} from 'react';

type AuthFormProps = {
    setIsLoggedin: React.Dispatch<React.SetStateAction<boolean>>;
  };
  

const AuthForm = ({setIsLoggedin}: AuthFormProps, setUsername: string ) => {
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
    const validateForm = (e: React.FormEvent) => {
        if (!formData.username.trim()) return 'Username is required';
        if (!isLogin && !formData.email.trim()) return 'Email is required';
        if (!formData.password.trim()) return 'Password is required';
        if (formData.password.length < 6) return 'Password must be at least 6 characters';
        return null;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        setSuccess('');

        const validationError = validateForm(e);
        if (validationError){
            setError (validationError);
            setIsLoading(false);
            return;
        }
        const signupData = {
            username: formData.username,
            email: formData.email,
            password: formData.password
        };
        
        const loginData = {
            username: formData.username,
            password: formData.password
        };

        try{
            const endpoint = isLogin ? '/api/auth/login' : '/api/auth/signup';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(isLogin ? loginData : signupData)
            });
            const data = await response.json();

            if (response.ok) {
                setSuccess (isLogin ? 'Login successful!' : 'Account created successfully!')
                if (isLogin){
                    setUsername (data.username);
                    setIsLoggedin(true);
                }    
            } else {
                setError(data.message || 'something went wrong');
            }
        }
        catch (err){
            setError('Network error. Please try again');
        }finally {
            setIsLoading(false);
        }
        
    };

    return (
        <div className="max-w-md mx-auto mt-12 p-6 bg-white rounded-lg shadow-md">
            <form onSubmit={handleSubmit} className="space-y-4">
                <h2 className="text-2xl font-bold text-center text-gray-800 mb-6"> 
                    {isLogin ? 'Login' : 'Signup'}
                </h2>
                {error && (
                    <div className= "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md">
                        {error}
                    </div>
                )}
                {success && (
                    <div className= "bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-md">
                        {success}
                    </div>
                )}
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                {!isLogin && (
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                )}
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
                    disabled={isLoading}
                    className={`w-full py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors ${
                        isLoading 
                            ? 'bg-gray-400 cursor-not-allowed' 
                            : 'bg-blue-500 hover:bg-blue-600 text-white'
                    }`}
                >
                    {isLoading ?(
                        <span className="flex items-center justify-center">
                            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        </span>
                    ) : (
                        isLogin ? 'Login' : 'Signup'
                    )}
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

