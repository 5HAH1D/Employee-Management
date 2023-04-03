-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 03, 2023 at 04:50 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `employee-management`
--

-- --------------------------------------------------------

--
-- Table structure for table `emp_data`
--

CREATE TABLE `emp_data` (
  `ID` varchar(10) NOT NULL,
  `fName` varchar(20) NOT NULL,
  `lName` varchar(20) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `JobPosition` varchar(50) NOT NULL,
  `Contact` varchar(20) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Address` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `emp_data`
--

INSERT INTO `emp_data` (`ID`, `fName`, `lName`, `Gender`, `JobPosition`, `Contact`, `Email`, `Address`) VALUES
('EMP01', 'Shahid', 'Saeed', 'Male', 'Senior Developer', '92300000000', 'example@123', 'Multan'),
('EMP02', 'fname', 'lname', 'Male', 'Accountant', '92300000000', 'example@1234', 'Multan'),
('EMP03', 'fname1', 'lname1', 'Male', 'Accountant', '92311111111', 'example@12', 'Lahore'),
('EMP04', 'fname2', 'lname2', 'Male', 'Accountant', '92322222222', 'employee4@123', 'Islamabad');

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `privilege` varchar(10) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_login`
--

INSERT INTO `user_login` (`privilege`, `user_name`, `password`) VALUES
('Admin', 'Admin', 'adam@123'),
('User', 'User1', 'user@123');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
