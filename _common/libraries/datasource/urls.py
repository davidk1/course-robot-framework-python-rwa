baseurls = {
    'rwa': 'http://localhost:3000',
    'rwa_api': 'http://localhost:3001'
}

endpoints = {
            'rwa_api': {
                'login': '/login',
                'bankAccounts': '/bankAccounts',
                'notifications': '/notifications',
                'notification_id': '/notifications/{}',
                'users': '/users',
                'transactions': '/transactions',
                'checkAuth': '/checkAuth',
                'logout': '/logout'
            }
}
