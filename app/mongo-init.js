db.createUser(
        {
            user: "appuser",
            pwd: "appuserpassword",
            roles: [
                {
                    role: "readWrite",
                    db: "logsdb"
                }
            ]
        }
);