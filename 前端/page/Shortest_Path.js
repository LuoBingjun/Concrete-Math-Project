// ����Ϊ��ʼ����յ㣬���ص�ֵΪ�ַ���"�������� ·���ڵ���� �ڵ��..."

// ʹ��ʾ��
closest_path(0, 490, function (var1) {
    console.info(var1);
});


function closest_path(var1, var2, callback) {
    var exec = require('child_process').exec;
    exec('python Shortest_Path.py ' + var1 + ' ' + var2, function (error, stdout, stderr) {
        if (stdout.length > 1) {
            callback(stdout);
        }
        if (error) {
            console.info('stderr : ' + stderr);
        }
    });
}
