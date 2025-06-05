const { generateSQL } = require('./src/main.gs');
describe('generateSQL', () => {
  it('should generate SQL for a given question', () => {
    const question = 'Get all users who registered yesterday';
    const result = generateSQL(question);
    console.log(result);
    expect(result.sql).toBe('SELECT * FROM users WHERE created_at >= CURDATE() - INTERVAL 1 DAY');
  });
});