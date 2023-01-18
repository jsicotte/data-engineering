module.exports = {
    checkAuth: (req, auth) => {},
    checkSqlAuth: (req, username) => {
      if (username === 'cube') {
        return {
          password: 'test',
          securityContext: {},
        };
      }
  
      throw new Error('Incorrect user name or password2');
    },
    preAggregationsSchema: `my_pre_aggregations`,
};