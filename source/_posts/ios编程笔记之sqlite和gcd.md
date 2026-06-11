---
title: iOS编程笔记之SQLite和GCD
date: 2015-01-05 12:00:00
categories: 技术
tags:
  - iOS
  - SQLite
  - GCD
  - FMDB
---

这里总结整理有关网络编程、sqlite数据库、GCD多线程的使用。

主要参考：

- [一个小时内学习 SQLite 数据库](http://www.jianshu.com/p/75eccda1c89f)
- [iOS学习之sqlite的创建数据库,表,插入查看数据](http://www.cnblogs.com/huangjianwu/archive/2011/11/28/2266583.html)
- [iOS 中sqlite 事务提交代码](http://blog.csdn.net/cuibo1123/article/details/39367027)
- [在iOS开发中使用FMDB](http://blog.devtang.com/blog/2012/04/29/use-fmdb/)

## SQLite数据库

### 简介

SQLite 是一个开源的嵌入式关系数据库，实现自包容、零配置、支持事务的SQL数据库引擎。其特点是高度便携、使用方便、结构紧凑、高效、可靠。与其他数据库管理系统不同，SQLite 的安装和运行非常简单，在大多数情况下 - 只要确保SQLite的二进制文件存在即可开始创建、连接和使用数据库。

### 一、使用原生的API

先加入sqlite开发库libsqlite3.dylib，相应类文件中导入头文件：

```objc
#import <UIKit/UIKit.h>
#import <sqlite3.h>

@interface ViewController : UIViewController
{
    sqlite3 *db;
}
@end
```

**常用方法：**

- `sqlite3 *db` - 数据库句柄，跟文件句柄FILE很类似
- `sqlite3_stmt *stmt` - 相当于ODBC的Command对象，用于保存编译好的SQL语句
- `sqlite3_open()` - 打开数据库，没有数据库时创建
- `sqlite3_exec()` - 执行非查询的sql语句
- `sqlite3_step()` - 在调用sqlite3_prepare后，使用这个函数在记录集中移动
- `sqlite3_close()` - 关闭数据库文件
- `sqlite3_column_text()` - 取text类型的数据
- `sqlite3_column_blob()` - 取blob类型的数据
- `sqlite3_column_int()` - 取int类型的数据

#### 1、添加库文件

添加libsqlite3.dylib库，导入头文件，添加成员变量db：

```objc
#import <UIKit/UIKit.h>
#import <sqlite3.h>

@interface ViewController : UIViewController
{
    sqlite3 *db;
}
@end
```

#### 2、打开数据库

```objc
NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
NSString *documents = [paths objectAtIndex:0];
NSString *database_path = [documents stringByAppendingPathComponent:DBNAME];

if (sqlite3_open([database_path UTF8String], &db) != SQLITE_OK) {
    sqlite3_close(db);
    NSLog(@"数据库打开失败");
}
```

#### 3、关闭数据库

```objc
sqlite3_close(db);
```

#### 4、更新数据

使用execu方法执行更新数值的sqlite语句，实现数据库的增、改、删：

```objc
-(void)execSql:(NSString *)sql
{
    char *err;
    if (sqlite3_exec(db, [sql UTF8String], NULL, NULL, &err) != SQLITE_OK) {
        sqlite3_close(db);
        NSLog(@"数据库操作数据失败!");
    }
}
```

#### 5、查询语句

```objc
NSString *sqlQuery = @"SELECT * FROM PERSONINFO";
sqlite3_stmt *statement;

if (sqlite3_prepare_v2(db, [sqlQuery UTF8String], -1, &statement, nil) == SQLITE_OK) {
    while (sqlite3_step(statement) == SQLITE_ROW) {
        char *name = (char*)sqlite3_column_text(statement, 1);
        NSString *nsNameStr = [[NSString alloc]initWithUTF8String:name];

        int age = sqlite3_column_int(statement, 2);

        char *address = (char*)sqlite3_column_text(statement, 3);
        NSString *nsAddressStr = [[NSString alloc]initWithUTF8String:address];

        NSLog(@"name:%@  age:%d  address:%@",nsNameStr,age, nsAddressStr);
    }
}
sqlite3_close(db);
```

#### 6、使用事务

对大批量、有制约关系的数据库操作，可以提高效率，而且数据库更安全。

### 二、使用第三方包FMDB

FMDB在使用上相当方便。以下是一个简单的例子：

```objc
NSString* docsdir = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) lastObject];
NSString* dbpath = [docsdir stringByAppendingPathComponent:@"user.sqlite"];
FMDatabase* db = [FMDatabase databaseWithPath:dbpath];
[db open];
FMResultSet *rs = [db executeQuery:@"select * from people"];
while ([rs next]) {
    NSLog(@"%@ %@",
        [rs stringForColumn:@"firstname"],
        [rs stringForColumn:@"lastname"]);
}
[db close];
```

#### FMDB使用说明

**1、引入相关文件**

将FMDB从github上clone下来，添加以下文件到工程中：

- FMDatabase.h / FMDatabase.m
- FMDatabaseAdditions.h / FMDatabaseAdditions.m
- FMDatabasePool.h / FMDatabasePool.m
- FMDatabaseQueue.h / FMDatabaseQueue.m
- FMResultSet.h / FMResultSet.m

**2、建立数据库**

```objc
FMDatabase *db = [FMDatabase databaseWithPath:@"/tmp/tmp.db"];
```

**3、打开数据库**

```objc
if (![db open]) {
    // error
    return;
}
// some operation
[db close];
```

**4、执行更新操作**

```objc
-[FMDatabase executeUpdate:error:withArgumentsInArray:orVAList:]
```

**5、执行查询操作**

```objc
FMResultSet *s = [db executeQuery:@"SELECT * FROM myTable"];
while ([s next]) {
    //retrieve values for each record
}
```

**6、数据类型获取**

FMDB提供以下方法获取不同类型的数据：
- `intForColumn:`
- `longForColumn:`
- `longLongIntForColumn:`
- `boolForColumn:`
- `doubleForColumn:`
- `stringForColumn:`
- `dateForColumn:`
- `dataForColumn:`

**7、数据参数**

```objc
NSString *sql = @"insert into User (name, password) values (?, ?)";
[db executeUpdate:sql, user.name, user.password];
```

**8、线程安全 - FMDatabaseQueue**

```objc
FMDatabaseQueue *queue = [FMDatabaseQueue databaseQueueWithPath:aPath];

[queue inDatabase:^(FMDatabase *db) {
    [db executeUpdate:@"INSERT INTO myTable VALUES (?)", [NSNumber numberWithInt:1]];
    // ...
}];

// 支持事务
[queue inTransaction:^(FMDatabase *db, BOOL *rollback) {
    [db executeUpdate:@"INSERT INTO myTable VALUES (?)", [NSNumber numberWithInt:1]];
    if (whoopsSomethingWrongHappened) {
        *rollback = YES;
        return;
    }
}];
```

## GCD多线程

### 什么是GCD

Grand Central Dispatch (GCD) 是Apple开发的一个多核编程的解决方法。该方法在Mac OS X 10.6雪豹中首次推出，并随后被引入到了iOS4.0中。

### dispatch queue分成以下三种

1. **Main queue** - 运行在主线程，通过 `dispatch_get_main_queue()` 获取
2. **并行队列 global dispatch queue** - 通过 `dispatch_get_global_queue` 获取，由系统创建三个不同优先级的dispatch queue
3. **串行队列 serial queues** - 一般用于按顺序同步访问，可创建任意数量的串行队列

### GCD的用法

```objc
// 后台执行：
dispatch_async(dispatch_get_global_queue(0, 0), ^{
    // something
});

// 主线程执行：
dispatch_async(dispatch_get_main_queue(), ^{
    // something
});

// 一次性执行：
static dispatch_once_t onceToken;
dispatch_once(&onceToken, ^{
    // code to be executed once
});

// 延迟2秒执行：
double delayInSeconds = 2.0;
dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, delayInSeconds * NSEC_PER_SEC);
dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
    // code to be executed on the main queue after delay
});

// 自定义dispatch_queue_t
dispatch_queue_t urls_queue = dispatch_queue_create("blog.devtang.com", NULL);
dispatch_async(urls_queue, ^{
    // your code
});
dispatch_release(urls_queue);

// 合并汇总结果
dispatch_group_t group = dispatch_group_create();
dispatch_group_async(group, dispatch_get_global_queue(0,0), ^{
    // 并行执行的线程一
});
dispatch_group_async(group, dispatch_get_global_queue(0,0), ^{
    // 并行执行的线程二
});
dispatch_group_notify(group, dispatch_get_global_queue(0,0), ^{
    // 汇总结果
});
```

### 应用举例 - 下载网页

```objc
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    NSURL * url = [NSURL URLWithString:@"http://www.baidu.com"];
    NSError * error;
    NSString * data = [NSString stringWithContentsOfURL:url encoding:NSUTF8StringEncoding error:&error];
    if (data != nil) {
        dispatch_async(dispatch_get_main_queue(), ^{
            NSLog(@"call back, the data is: %@", data);
        });
    } else {
        NSLog(@"error when download:%@", error);
    }
});
```

### 后台长久运行

GCD可以让程序在后台较长久的运行（最多10分钟）：

```objc
// AppDelegate.h
@property (assign, nonatomic) UIBackgroundTaskIdentifier backgroundUpdateTask;

// AppDelegate.m
- (void)applicationDidEnterBackground:(UIApplication *)application
{
    [self beingBackgroundUpdateTask];
    // 在这里加上你需要长久运行的代码
    [self endBackgroundUpdateTask];
}

- (void)beingBackgroundUpdateTask
{
    self.backgroundUpdateTask = [[UIApplication sharedApplication] beginBackgroundTaskWithExpirationHandler:^{
        [self endBackgroundUpdateTask];
    }];
}

- (void)endBackgroundUpdateTask
{
    [[UIApplication sharedApplication] endBackgroundTask: self.backgroundUpdateTask];
    self.backgroundUpdateTask = UIBackgroundTaskInvalid;
}
```

## 参考资料

- [iOS多线程GCD](http://www.cnblogs.com/pure/archive/2013/03/31/2977421.html)
- [使用GCD](http://blog.csdn.net/eduora_ke/article/details/42164765)
- [FMDB官方使用文档](https://github.com/ccgus/fmdb)
